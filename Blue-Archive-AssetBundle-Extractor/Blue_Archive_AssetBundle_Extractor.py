import UnityPy
import glob
import os

from UnityPy.classes import AudioClip, Mesh, TextAsset

required_unitypy_version = '1.10.14'
if UnityPy.__version__ != required_unitypy_version:
    raise ImportError(f"Invalid UnityPy version detected. Please use version {required_unitypy_version}")

export_target_type_array = ["Texture2D", "Sprite", "AudioClip", "Mesh", "TextAsset"]

path = input("Enter the path to AssetBundls: ").replace("\"", "")
output_path = input("Enter the path to output: ").replace("\"", "")
print("Copying start")
print("If an exception occurs during copying, the log is displayed but the process is not aborted")

for bundle_path in glob.glob(os.path.join(path, "*")):
    env = UnityPy.load(bundle_path)
    
    for path, obj in env.container.items():
        try:
            if not obj.type.name in export_target_type_array:
                continue
            
            full_path_dir_str = os.path.join(output_path, *path.split("/")[:-1]) # �t�@�C�������������t���p�X
            os.makedirs(full_path_dir_str, exist_ok=True) # �t�H���_�����
            
            data = obj.read()
            match obj.type.name:
                case "Texture2D" | "Sprite":
                    data.image.save(os.path.join(full_path_dir_str, data.name + ".png")) # �g���q��PSD���Ɨ�O���o��̂�splitext�Ŋg���q���̂������p�X��.png���������ĕۑ�
                    
                case "AudioClip":
                    for name, audio_data in data.samples.items():
                        with open(os.path.join(full_path_dir_str, name), "wb") as f:
                            f.write(audio_data)
                        
                case "Mesh":
                    with open(os.path.join(full_path_dir_str, f"{data.name}.obj"), "wt", newline = "") as f:
                        # newline = "" is important
                        f.write(data.export())
                        
                case "TextAsset":
                    with open(os.path.join(full_path_dir_str, data.name), "wb") as f:
                        f.write(bytes(data.script))
                    
        except Exception as e:
            print(f"Exception occurred on {env.file.name}:")
            print(e)
            
print("Done")