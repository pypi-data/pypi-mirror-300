import datetime
import numpy as np
import os
import onnx
import onnxruntime


class InferenceSession(onnxruntime.InferenceSession):
    def __init__(
        self,
        path_or_bytes: str | bytes | os.PathLike,
        **kwargs,
    ) -> None:
        # 获取模型名称
        if isinstance(path_or_bytes, (str, os.PathLike)):
            self.model_name = os.path.basename(path_or_bytes)
        else:
            self.model_name = "model"
        # 创建影子Session
        self.model = onnx.load(path_or_bytes)
        # 修改模型输出节点tag
        for node in self.model.graph.node:
            for output in node.output:
                self.model.graph.output.extend([onnx.ValueInfoProto(name=output)])
        self.ShadowSession = onnxruntime.InferenceSession(
            self.model.SerializeToString()
        )
        super().__init__(path_or_bytes, **kwargs)

    def run(
        self,
        output_names,
        input_feed,
        run_options=None,
        dump_path: str | os.PathLike = None,
    ):
        # 调用父类的run方法
        super_results = super().run(output_names, input_feed, run_options)
        # 调用影子Session的run方法
        outputs = [x.name for x in self.ShadowSession.get_outputs()]
        ort_outs = self.ShadowSession.run(outputs, input_feed, run_options)
        # 生成字典，便于查找层对应输出
        ort_outs = dict(zip(outputs, ort_outs))
        # numpy写出到文件
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{self.model_name}_{date}"
        np.savez(dump_path if dump_path else file_name, **ort_outs)
        return super_results
