function previewImage(event) {
  const input = event.target;
  const file = input.files[0];
  const preview = document.getElementById("image-preview");
  const icon = document.getElementById("upload-icon");

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      preview.src = e.target.result;
      preview.classList.remove("hidden");
      icon.classList.add("hidden");
    };
    reader.readAsDataURL(file);
  }
}
