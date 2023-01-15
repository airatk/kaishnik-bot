from os import walk, path, remove


def export_source_code_to_txt(source_code_path: str, txt_file: str):
	for (directory, _, files) in walk(source_code_path):
		files = [ file for file in files if file.endswith(".py") ]

		for file in files:
			filepath: str = path.join(directory, file)

			with (
				open(file=filepath, mode="r") as source_file,
				open(file=txt_file, mode="a") as destination_file
			):
				destination_file.writelines([
					f"# {filepath}\n",
					"\n",
					source_file.read().replace("\n\n\n", "\n\n"),
					"\n\n"
				])

def remove_txt_file(txt_file):
	if not path.exists(txt_file): return
	
	remove(txt_file)


if __name__ == "__main__":
	txt_file: str = "source_code.txt"
	source_code_path: str = "bot/patforms"

	remove_txt_file(txt_file)
	export_source_code_to_txt(source_code_path, txt_file)
