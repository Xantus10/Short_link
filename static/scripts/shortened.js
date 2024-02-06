function copy() {
  let copyText = document.getElementById("urlaft").innerHTML;
  navigator.clipboard.writeText(copyText);
}