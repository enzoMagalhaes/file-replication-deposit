//const socket = new WebSocket("ws://localhost:8000");
const dropArea = document.getElementById('dropArea');
const fileList = document.querySelector('#fileList ul');
let uploadedFiles = [];
let requestedFiles=[];
let message = "";

// socket.onopen = () => {
//     console.log("WebSocket connection established.");
//   };
  
// socket.onmessage = (event) => {
//     const responseElement = document.getElementById("response");
//     responseElement.textContent = event.data;
//   };
  
// socket.onerror = (error) => {
//     console.error("WebSocket error:", error);
//   };
  
// socket.onclose = () => {
//     console.log("WebSocket connection closed.");
//   };



// Prevent default browser behavior for drag events
dropArea.addEventListener('dragenter', preventDefaults, false);
dropArea.addEventListener('dragover', preventDefaults, false);
dropArea.addEventListener('dragleave', preventDefaults, false);
dropArea.addEventListener('drop', preventDefaults, false);

// Highlight drop area when a file is dragged over it
dropArea.addEventListener('dragenter', highlight, false);
dropArea.addEventListener('dragover', highlight, false);
dropArea.addEventListener('dragleave', unhighlight, false);

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);

// Prevent default behavior for drag events
function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

// Add highlight class when a file is dragged over the drop area
function highlight() {
  dropArea.classList.add('highlight');
}

// Remove highlight class when a file is dragged out of the drop area
function unhighlight() {
  dropArea.classList.remove('highlight');
}

// Handle dropped files
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
  
    // Process each dropped file
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const listItem = document.createElement('li');
      listItem.textContent = file.name;
      fileList.appendChild(listItem);
      uploadedFiles.push(file);
    }
  }

function handleUpload() {
    console.log(uploadedFiles);
    for (let i = 0; i < uploadedFiles.length; i++) {
      const file = uploadedFiles[i];
      uploadFile(file); // Implement file upload logic here
    }
  }
// Implement file upload logic
function uploadFile(file) {
    // Add your file upload logic here
    console.log('Uploading file:', file.name);
  }


let submittedNumber = null;
// Get references to the elements
const numberInput = document.getElementById('numberInput');
const submitButton = document.getElementById('submitButton');
const searchInput = document.getElementById('searchInput');
const browseButton = document.getElementById('browseButton');

browseButton.addEventListener('click', function(){
    const enteredString = searchInput.value;
    console.log("Search bar:", enteredString)

});

uploadButton.addEventListener('click', function() {
    const enteredNumber = parseInt(numberInput.value, 10);
    // Check if the entered value is a valid number
    if (!isNaN(enteredNumber)) {
      submittedNumber = enteredNumber;
      console.log('Submitted number:', submittedNumber);
      
      // Call a function or perform any desired action with the submitted number
      // For example:
      // myFunction(submittedNumber);
    } else {
      console.log('Invalid number entered.');
      // Handle case when an invalid number is entered
    }
    handleUpload();
  });
