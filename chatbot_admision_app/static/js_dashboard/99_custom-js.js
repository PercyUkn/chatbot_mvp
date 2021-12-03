let logoutButton = document.getElementById("logout_button");
logoutButton.addEventListener("click", function () {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/logout", false); // false for synchronous request
    console.log("clicked")
    xmlHttp.send(null);
    window.location.replace("http://localhost:5000");
    return xmlHttp.responseText;
});