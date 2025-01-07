const API_URL = "http://127.0.0.1:8000";
const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");

async function fetchFiles() {
  try {
    const response = await fetch(`${API_URL}/list`);
    const files = await response.json();

    console.log("Files:", files);

    displayFiles(files);
  } catch (error) {
    console.error("Error fetching files:", error);
  }
}

function displayFiles(files) {
  fileList.innerHTML = "";
  files.forEach((file) => {
    const li = document.createElement("li");
    li.innerHTML = `${file.filename} (por: ${file.uploader}) 
                    <div>
                    <button onclick="handleDownload(${file.id}, '${file.filename}')">Download</button>
                    <button onclick="handleDelete(${file.id})">Deletar</button>
                    <button onClick="handleView('${API_URL}/uploads/${file.filename}')">Visualizar</button>
                    </div>`;
    fileList.appendChild(li);
  });
}

async function handleView(filepath) {
  window.open(filepath, "_blank");
}

async function handleFileUpload(event) {
  event.preventDefault();
  const selectedFile = fileInput.files[0];
  if (!selectedFile) {
    return alert("Please select a file to upload");
  }

  const fileNameInput = document.getElementById("fileName").value;
  if (!fileNameInput) {
    return alert("Please enter a file name");
  }
  const fileUploader = document.getElementById("fileUploader").value;
  if (!fileUploader) {
    return alert("Please enter your name");
  }

  const fileExtension = selectedFile.name.substring(
    selectedFile.name.lastIndexOf(".")
  );
  const fileName = `${fileNameInput}${fileExtension}`;

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("fileName", fileName);
  formData.append("uploader", fileUploader);

  try {
    await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
    });
    fileInput.value = "";
    document.getElementById("fileName").value = "";
    document.getElementById("fileUploader").value = "";
    fetchFiles();
  } catch (error) {
    console.error("Error uploading file:", error);
  }
}

function handleDownload(fileId, filename) {
  fetch(`${API_URL}/download/${fileId}`)
    .then((response) => response.blob())
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    })
    .catch((error) => {
      console.error("Error downloading file:", error);
    });
}

async function handleDelete(fileId) {
  try {
    const response = await fetch(`${API_URL}/delete/${fileId}`, {
      method: "DELETE",
    });
    const result = await response.json();
    if (response) {
      fetchFiles();
    }
  } catch (error) {
    console.error("Error deleting file:", error);
  }
}

uploadForm.addEventListener("submit", handleFileUpload);

// Fetch files on page load
fetchFiles();
