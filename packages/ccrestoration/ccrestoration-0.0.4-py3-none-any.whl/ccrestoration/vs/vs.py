from typing import Any, Callable, Union

import numpy as np
import torch
import vapoursynth as vs


def frame_to_tensor(frame: vs.VideoFrame, device: torch.device) -> torch.Tensor:
    return torch.stack(
        [torch.from_numpy(np.asarray(frame[plane])).to(device) for plane in range(frame.format.num_planes)]
    ).clamp(0.0, 1.0)


def tensor_to_frame(tensor: torch.Tensor, frame: vs.VideoFrame) -> vs.VideoFrame:
    array = tensor.squeeze(0).detach().cpu().numpy()
    for plane in range(frame.format.num_planes):
        np.copyto(np.asarray(frame[plane]), array[plane])
    return frame


def inference_sr(
    inference: Callable[[torch.Tensor], torch.Tensor],
    clip: vs.VideoNode,
    scale: Union[float, int, Any],
    device: torch.device,
    _frame_to_tensor: Callable[[vs.VideoFrame, torch.device], torch.Tensor] = frame_to_tensor,
    _tensor_to_frame: Callable[[torch.Tensor, vs.VideoFrame], vs.VideoFrame] = tensor_to_frame,
) -> vs.VideoNode:
    """
    Inference the video with the model, the clip should be a vapoursynth clip

    :param inference: The inference function
    :param clip: vs.VideoNode
    :param scale: The scale factor
    :param device: The device
    :param _frame_to_tensor: The function to convert the frame to tensor
    :param _tensor_to_frame: The function to convert the tensor to frame
    :return:
    """

    if not isinstance(clip, vs.VideoNode):
        raise vs.Error("Only vapoursynth clip is supported")

    if clip.format.id not in [vs.RGBH, vs.RGBS]:
        raise vs.Error("Only vs.RGBH and vs.RGBS formats are supported")

    def _inference(n: int, f: list[vs.VideoFrame]) -> vs.VideoFrame:
        img = _frame_to_tensor(f[0], device).unsqueeze(0)

        output = inference(img)

        return _tensor_to_frame(output, f[1].copy())

    new_clip = clip.std.BlankClip(width=clip.width * scale, height=clip.height * scale, keep=True)
    return new_clip.std.FrameEval(
        lambda n: new_clip.std.ModifyFrame([clip, new_clip], _inference), clip_src=[clip, new_clip]
    )
