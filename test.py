# Below is an srt file, please adjust the transcribed text to make the pause more nature and friendly. Also change the timestamp accordingly 

import json
from datetime import datetime, timedelta
import pysrt


def convert_time(data):
    seconds, milliseconds = map(int, str(data).split('.'))
    # 使用timedelta来表示毫秒部分
    time_delta = timedelta(seconds=seconds, milliseconds=milliseconds)
    base_time = datetime(2000, 1, 1)

    # 添加时间差到基准时间
    result_time = base_time + time_delta

    # 格式化输出，保留三位有效数字
    result_str = result_time.strftime("%H:%M:%S.%f")[:-3]

    return result_str


def hf_pipeline_to_srt(json_result, output_file=None):
    result = json_result
    file = pysrt.SubRipFile()
    for idx, chk in enumerate(result["chunks"]):
        text = chk["text"]
        start, end = map(convert_time, chk["timestamp"])
        # print(start)
        
        sub = pysrt.SubRipItem(idx, 
            start=start, end=end, text=text.strip())
        file.append(sub)
        
    if output_file is not None:
        # print(file)
        print(f"Saved to {output_file}")
        file.save(output_file)
        return output_file
    else:
        import io
        fp = io.StringIO("")
        file.write_into(fp)
        result = fp.getvalue()
        return result


if __name__ == "__main__":
    with open("tmp.json", "r") as fp:
        result = json.load(fp)
    hf_pipeline_to_srt(result, output_file="tmp.srt")