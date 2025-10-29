import dashscope
from dashscope import Generation
import base64
import requests
import os
import json

#API密钥
dashscope.api_key = "sk-5a1604b37f774ec5a85d1ab4a4c21534"  

def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_video_from_image(image_path, prompt, negative_prompt="", num_frames=16):
    image_base64 = image_to_base64(image_path)
    #请求参数
    messages = [{
        'role': 'user',
        'content': [
            {
                'image': image_base64,
                'text': prompt
            }
        ]
    }]
    
    #image_path: 输入图片的路径    prompt: 生成视频的文本描述     negative_prompt: 负面提示词     num_frames: 生成的视频帧数
    
    try:
        response = Generation.call(
            model='tongyi-video-2.2',
            messages=messages,
            video_length=num_frames, 
            negative_prompt=negative_prompt
        )
        
        if response.status_code == 200:
            video_url = response.output.video_url
            video_response = requests.get(video_url)
            if video_response.status_code == 200:
                output_path = 'output_video.mp4'
                with open(output_path, 'wb') as video_file:
                    video_file.write(video_response.content)
                print(f"视频已成功生成并保存至: {output_path}")
                return output_path
            else:
                print("下载视频失败")
                return None
        else:
            print(f"生成视频失败: {response.message}")
            return None
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None


if __name__ == "__main__":
    image_path = "input_image.jpg"  
    prompt = "生成一个图片中的人正在打篮球的视频"
    negative_prompt = "模糊的、质量差的"
    
    output_video = generate_video_from_image(
        image_path=image_path,
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_frames=16
    )
    
    if output_video:
        print("视频生成成功")
    else:
        print("视频生成失败")