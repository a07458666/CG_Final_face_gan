var img;
const model_url = "./cycleGan/";

const imagePreview = document.querySelector('#image_preview');
const imageResult = document.querySelector('#image_result');
const selectedModel = document.querySelector('#models');
const fileUploader = document.querySelector('#image_uploader');
const upload_button = document.getElementById("upload_button");

fileUploader.addEventListener('change', handle_file);

// preview image
async function handle_file(e){
	const file = e.target.files[0];
	if (!file) return;
	show_image(file);
}
function show_image(fileObj){
	img = fileObj;
	imagePreview.src = URL.createObjectURL(fileObj);
}
// upload image
upload_button.onclick = 
async function upload(){
	try{
		const check = await check_file(img);
		if(!check.isValid)throw check.errorMessages;
		
		const array_buffer = await get_array_buffer(img);
		const data = await post(array_buffer);
    show_result(data);
	}
	catch(err){
		alert(err);
	}
}
function check_file(fileObject) {
  return new Promise(resolve => {
    const validFileTypes = ["image/jpg", "image/jpeg"];
    const isValidFileType = validFileTypes.includes(fileObject.type);
    let errorMessages = [];

    if (!isValidFileType) {
      errorMessages.push("You can only upload jpg or jpeg file!");
    }

    const isValidFileSize = fileObject.size < (1024*1024*5);
    if (!isValidFileSize) {
      errorMessages.push("Image must smaller than 5MB!");
    }

    resolve({
      isValid: isValidFileType && isValidFileSize,
      errorMessages: errorMessages.join("\n")
    });
  });
}
function get_array_buffer(fileObj) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    // Get ArrayBuffer when FileReader on load
    reader.addEventListener("load", () => {
      resolve(reader.result);
    });

    // Get Error when FileReader on error
    reader.addEventListener("error", () => {
      reject("error occurred in getArrayBuffer");
    });

    reader.readAsArrayBuffer(fileObj);
  });
}
function post(arrayBuffer) {
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	
	return fetch(model_url, {
		headers: {
			version: 1,
			"content-type": "application/json",
			"X-CSRFToken": csrftoken
		},
		method: "POST",
		body: JSON.stringify({
			img: Array.from(new Uint8Array(arrayBuffer)),
			model: selectedModel.value
		})
	}).then(result => {
		if (!result.ok) {
			throw res.statusText;
		}
		return result.json();
  }).then(data => data).catch(err => console.log("err", err));
}
function show_result(data){
  imageResult.src = 'data:image/jpg;base64, ' + data.base64_img;
}