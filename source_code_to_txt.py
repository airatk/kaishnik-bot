from os import walk, path


with open(file="destination_file.txt", mode="w") as destination_file:
	for (directory, _, files) in walk("bot/platforms"):
		for file in files:
			if not file.endswith(".py"): continue

			filepath = path.join(directory, file)

			with open(file=filepath, mode="r") as opened_file:
				destination_file.writelines([
					f"# {filepath}\n",
					"\n",
					opened_file.read().replace("\n\n\n", "\n\n"),
					"\n\n"
				])
