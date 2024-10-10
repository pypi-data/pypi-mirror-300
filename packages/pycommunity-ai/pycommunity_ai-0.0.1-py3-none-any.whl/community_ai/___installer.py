import urllib.request
import os

def install(
    model:str,*,
    path: str="./models",
    source: str=None,
    quiet: bool=False,
    force: bool=False
):
    os.mkdir(f"{path}/{model}", )
    trusted = False
    download_url = ""
    if source == None:
        download_url = f"https://github.com/CommunityAIs/ai-test/blob/main"
        trusted = True
    else:
        source = source.replace("{{model}}")
        download_url = source
    if not trusted and not quiet:
        print("WARNING: Downloading from not trustet source!")
    error = False
    urllib.request.urlretrieve(f"{download_url}/nn.ai", f"{path}/{model}/nn.ai")
    try:
        urllib.request.urlretrieve(f"{download_url}/LICENSE", f"{path}/{model}/LICENSE")
    except:
        error = True
    try:
        urllib.request.urlretrieve(f"{download_url}/README.md", f"{path}/{model}/README.md")
    except:
        error = True
    

    if force and error:
        raise Exception("[ERROR] can not downloading all files, force = True")
    
    
    
    

    