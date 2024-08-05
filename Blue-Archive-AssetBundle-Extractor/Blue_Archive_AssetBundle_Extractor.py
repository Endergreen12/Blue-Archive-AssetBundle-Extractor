from tkinter.font import Font
import UnityPy
import glob
import os

from UnityPy.classes import AudioClip, Mesh, TextAsset

required_unitypy_version = '1.10.14'
if UnityPy.__version__ != required_unitypy_version:
    raise ImportError(f"Invalid UnityPy version detected. Please use version {required_unitypy_version}")

path = input("Enter the path to AssetBundls: ").replace("\"", "")
output_path = input("Enter the path to output: ").replace("\"", "")
print("Copying start")
print("If an exception occurs during copying, the log is displayed but the process is not aborted")

for bundle_path in glob.glob(os.path.join(path, "*")):
    env = UnityPy.load(bundle_path)
    
    for path, obj in env.container.items():
        try:
            path_array = path.split("/")
            full_path_str = os.path.join(output_path, *path_array)
            full_path_without_filename_str = os.path.join(output_path, *path_array[:-1]) # path_array[:-1]でファイル名を除く
            os.makedirs(full_path_without_filename_str, exist_ok=True) # フォルダを作る
            
            match obj.type.name:
                case "Texture2D" | "Sprite":
                    data = obj.read()
                    data.image.save(os.path.splitext(full_path_str)[0] + ".png") # 拡張子がPSDだと例外が出るのでsplitextで拡張子をのぞいたパスに.pngをくっつけて保存
                    
                case "AudioClip":
                    clip : AudioClip = obj.read()
                    for name, data in clip.samples.items():
                        with open(os.path.join(full_path_without_filename_str, name), "wb") as f:
                            f.write(data)
                            
                case "Font":
                    font : Font = obj.read()
                    
                    extension = ""
                    
                    if font.m_FontData:
                        extension = ".ttf"
                        
                    if font.m_FontData[0:4] == b"OTTO":
                        extension = ".otf"

                    with open(os.path.join(full_path_without_filename_str, font.name + extension), "wb") as f:
                        f.write(font.m_FontData)
                        
                case "Mesh":
                    mesh : Mesh = obj.read()
                    with open(os.path.join(full_path_without_filename_str, f"{mesh.name}.obj"), "wt", newline = "") as f:
                        # newline = "" is important
                        f.write(mesh.export())
                        
                case "TextAsset":
                    data : TextAsset = obj.read()
                    with open(full_path_str, "wb") as f:
                        f.write(bytes(data.script))

                    
        except Exception as e:
            print(f"Exception occurred on {env.file.name}:")
            print(e)
            
print("Done")