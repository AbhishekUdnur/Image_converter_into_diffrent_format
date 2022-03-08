from bottle import Bottle, route, run, template, static_file
from bottle import abort, get, post, request, response
from bottle import redirect, static_file
import os
from PIL import Image


converter = Bottle()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def get_save_path_with_format(filename, extension):
	if not extension.startswith('.'):
		extension = '.' + extension
	return ''.join(_ for _ in [BASE_DIR, '/media/', filename, extension])


@converter.route('/', method='GET')
def get_form():
    return '''
		<head>
			<link
			href="https://fonts.googleapis.com/css?family=Raleway:400,600&display=swap"
			rel="stylesheet">
		</head>
		<body>
	    	<div class="wrapper">
				<h2><strong>IMAGE_FORMAT_CONVERTER</strong></h2>
				<form action="/"
				method="post" enctype="multipart/form-data">
					<div>
					Optional name: <br/> <input type="text" name="optional_name" />
					</div>
					<div>
					Select a file: <br/> <input type="file" name="upload" />
					</div>
					<select name="output_file" id="out">
					<option value="gif">GIF</option>
					<option value="png">PNG</option>
					<option value="jpeg">JPEG</option>
					<option value="webp">WEBP</option>
					<option value="jpg">jpg</option>
					</select>
					<br/>
					<input class='button'
					type="submit" value="Start upload" />
				</form>
			</div>
		</body>
		<style>
		body {
			font-family: 'Raleway', sans-serif;
			padding: 70px;
			color: #EFC20E;
		}
		h3 {
			color: #EFC20E;
		}
		.wrapper {
			margin-top: 30px;
			background-color: #6B695D;
			margin: 0 auto;
			max-width: 50%;
			padding: 100px;
		  	align-items: center;
			text-align: center;
		  	justify-content: center;
			box-shadow: 0 10px 7px -6px black;
			border-radius: 2px;
		}
		form {
			margin-top: 20px;
			display: block;
		}
		input {
			margin: 20px;
			font-size: 14px;
		}
		.button {
			padding: 15px 25px 15px 25px;
			background-color: #EFC20E;
			color: white;
			border: 0;
			border-radius: 2px;
			font-family: 'Raleway', sans-serif;
			font-size: 14px;
			font-weight: 600;
		}
		<style>
		'''


@converter.route('/', method='POST')
def do_upload():
	quality = 100
	optional_name = request.forms.get('optional_name')
	uploaded = request.files.get('upload')
	out_file_ext = request.forms.get('output_file')
	print(out_file_ext)
	name, ext = os.path.splitext(uploaded.filename)
	if ext.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
	    return 'File extension not allowed.'

	if optional_name != '':
	    name = optional_name

	save_path = get_save_path_with_format(name, ext)

	try:
	    uploaded.save(save_path + ext)
	except IOError:
	    os.remove(save_path + ext)
	    uploaded.save(save_path + ext)
	
	try:
		
		if ext.lower() not in ('.png', '.jpg', '.webp', '.gif'):
			
			try:
				pass
				
			except OSError:
				im = Image.open(save_path + ext)
				e = im.convert('RGB')
				output_path = get_save_path_with_format(name, '.'+out_file_ext)
				e.save(output_path.split('.')[0] +'.' + 'jpeg')
				os.remove(save_path + ext)
				redirect("/converted/%s" % name + '.'+out_file_ext)
		else:
			im = Image.open(save_path + ext)
			output_path = get_save_path_with_format(name, '.'+out_file_ext)
			im.save(output_path, out_file_ext, quality=quality)
			os.remove(save_path + ext)
			redirect("/converted/%s" % name + '.'+out_file_ext)
	
	except KeyError:
		
		im = Image.open(save_path + ext)
		e = im.convert('RGB')
		output_path = get_save_path_with_format(name, '.'+out_file_ext)
		e.save(output_path.split('.')[0] +'.' + 'jpg')
		os.remove(save_path + ext)
		redirect("/converted/%s" % name + '.'+out_file_ext)

@converter.route('/download/<filename:path>')
def send_image(filename):
	print('filename - ',filename)
	return static_file(filename,root='/', download=filename)

@converter.route('/converted/<filename:path>')
def updloaded(filename):
    return static_file(
        filename,
        root=BASE_DIR + '/media',
        mimetype='image/webp')


run(converter, host='localhost', port='8080', debug=True)

