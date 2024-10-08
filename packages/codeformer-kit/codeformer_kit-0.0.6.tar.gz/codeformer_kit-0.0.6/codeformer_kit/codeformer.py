import os
import torch
import numpy as np
from torchvision.transforms.functional import normalize

from datvtn_nn_kit.nn import img_to_tensor, tensor_to_img
from datvtn_nn_kit.utils import load_file_from_url
from codeformer_kit.archs.codeformer_arch import CodeFormer

class CodeformerProcessor:
    def __init__(self, model_dir: str = "./checkpoints", device: torch.device = None):
        model_url = "https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth"
        model_path = os.path.join(model_dir, "codeformer.pth")

        if not os.path.exists(model_path):
            load_file_from_url(url=model_url, model_dir=model_dir, progress=True, file_name=None)

        self._device = device if device is not None else torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

        self.model = CodeFormer(
                        dim_embd=512,
                        codebook_size=1024,
                        n_head=8,
                        n_layers=9,
                        connect_list=["32", "64", "128", "256"],
                    ).to(self._device)

        checkpoint = torch.load(model_path)["params_ema"]
        self.model.load_state_dict(checkpoint)
        self.model.eval()

    def process(self, cropped_face: np.ndarray, fidelity: float = 0.5):
        cropped_face_t = img_to_tensor(
            cropped_face / 255.0, bgr2rgb=True, float32=True
        )
        normalize(cropped_face_t, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), inplace=True)
        cropped_face_t = cropped_face_t.unsqueeze(0).to(self._device)

        try:
            with torch.no_grad():
                output = self.model(
                    cropped_face_t, w=fidelity, adain=True
                )[0]
                restored_face = tensor_to_img(output, rgb2bgr=True, min_max=(-1, 1))
            del output
            torch.cuda.empty_cache()
        except RuntimeError as error:
            print(f"Failed inference for CodeFormer: {error}")
            restored_face = tensor_to_img(
                cropped_face_t, rgb2bgr=True, min_max=(-1, 1)
            )

        restored_face = restored_face.astype("uint8")
        return restored_face
