from flask import Flask, jsonify, request
from gradio_client import Client
import trimesh, random

client = Client("https://hysts-shap-e.hf.space/")

def object_generate(prompt):
	seed = 0 #random.randint(0, 2147483647)
	result = client.predict(prompt,	# str  in 'Prompt' Textbox component
							seed,	# int | float (numeric value between 0 and 2147483647) in 'Seed' Slider component
							20,	# int | float (numeric value between 1 and 20) in 'Guidance scale' Slider component
							64,	# int | float (numeric value between 1 and 100) in 'Number of inference steps' Slider component
							api_name="/text-to-3d")
	return result	



def generate_list_of_objects(objects_list, saving_path):
	n = 0
	for name in objects_list:
		result = object_generate(name)
		mesh = trimesh.load(result)
		#saving_path = "/Users/wangyutong/ProjectDev/immersive_project/try/objects/"
		mesh.export(file_type="obj", file_obj=saving_path + name + '.obj')
		n += 1

	return n

app = Flask(__name__)

@app.route("/shap_e/status", methods = ["GET"])
def status():
	return jsonify(status = "ok")

@app.route("/shap_e/user_input", methods = ['POST'])
def getUserPrompt():
    prompt = request.json
    objects = prompt['objects']
    saving_path = prompt['saving_path']
    objects_list = objects.split(",")
    n = generate_list_of_objects(objects_list, saving_path)
    return  {'amount of objects generated':n}





if __name__ == '__main__':
    app.run(port = 7777)
