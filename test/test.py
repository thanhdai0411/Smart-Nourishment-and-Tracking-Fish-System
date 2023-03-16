import os 
BASE_PATH = "D:/Studyspace/DoAn/Aquarium"

FOLDER_SAVE_IMAGES =BASE_PATH+ "/coco128/images/train2017"
FOLDER_SAVE_LABELS =BASE_PATH+ "/coco128/labels/train2017"

PATCH_TO_COCO12YAML = BASE_PATH + "/data/coco128.yaml"


name_fish = "FishGold"


# delete image 
for images in os.listdir(FOLDER_SAVE_IMAGES):
	base_path = FOLDER_SAVE_IMAGES + "/"
	name_image = images.split('_')[0]

	if(name_image.strip() == name_fish) :
		os.remove(base_path + images)
	
# delete label 
for labels in os.listdir(FOLDER_SAVE_LABELS):
	base_path = FOLDER_SAVE_LABELS + "/"

	name_image = labels.split('_')[0]

	if(name_image.strip() == name_fish) :
		os.remove(base_path + labels)

# rewrite file coco128.yaml
saveCoco128Read = open(PATCH_TO_COCO12YAML, 'r')
WHITE_SPACE = "    "

a = saveCoco128Read.read()

if a:

	b = a.split("\n")
	b.pop()

	c = len(b)
	d = b[c - 1]

	e = d.split(":")

	f = e[0].strip()
	g = e[1].strip()

	listLabel = b[3:]

	
	for item in listLabel:
		e = item.split(":")
		if(e[1].strip() == name_fish) :
			b.remove(item)
			listLabel.remove(item)
	

	if len(b) > 3 :

	
		coco128 = [
				'train: ' + FOLDER_SAVE_IMAGES, 'val: ' + FOLDER_SAVE_IMAGES, 'names:']
		
		for index, item in enumerate(listLabel):
			e = item.split(":")
			new = WHITE_SPACE + str(index) + ": " + e[1].strip()
			coco128.append(new)


		saveCoco128Write = open(PATCH_TO_COCO12YAML, 'w')

		for value in coco128:
			saveCoco128Write.write(value)
			saveCoco128Write.write('\n')
		saveCoco128Write.close()
		

		# update index label 
		newCocoYaml = open(PATCH_TO_COCO12YAML, 'r').read()
		list_new = newCocoYaml.split("\n")
		list_new.pop()

		newListLabel = list_new[3:]
		print(newListLabel)

		for item in (newListLabel):
			e = item.split(":")
			
			index_label = e[0].strip()
			name_label = e[1].strip()
			# delete label 
			for labels in os.listdir(FOLDER_SAVE_LABELS):
				base_path = FOLDER_SAVE_LABELS + "/"
				name_image = labels.split('_')[0]

				data_file = open(base_path + labels , 'r').read()
				if(name_image == name_label) :
					read_file = data_file.split(" ")
					read_file[0] = str(index_label)
				
					my_string = " "
					for x in read_file :
						my_string+= " " + x
					open(base_path + labels , 'w').write(my_string.strip())
	else :
		open(PATCH_TO_COCO12YAML, 'w').write("")


	