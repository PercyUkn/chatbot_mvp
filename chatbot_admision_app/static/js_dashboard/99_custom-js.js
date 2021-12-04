current_domain = window.location.hostname
current_url = window.location.href
current_path = window.location.pathname
index_substring = current_url.indexOf(current_path)
base_url = current_url.substring(0, index_substring)
let logoutButton = document.getElementById("logout_button");
logoutButton.addEventListener("click", function () {
    let xmlHttp = new XMLHttpRequest();
    let endpoint = base_url + "/logout"
    console.log(current_domain)
    console.log(endpoint)
    xmlHttp.open("GET", endpoint, false); // false for synchronous request
    console.log("clicked")
    xmlHttp.send(null);
    window.location.replace(base_url);
    return xmlHttp.responseText;
});