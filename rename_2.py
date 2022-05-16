from pathlib import Path


if __name__ == "__main__":
	'''
		将目录中的文件名字中的'（2）' 变换成  '_2'， eg: A (2).jpg  --> A_2.jpg
	'''
	dir = 'JPEGImages'
	[img.rename(f"{dir}/{img.name}".replace(" (2)", "_2")) for img in Path(dir).iterdir()]