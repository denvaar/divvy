var created = false;
var addAccountForm = document.getElementById("accountCreate");

function overlay() {
  el = document.getElementById("overlay");
  el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
  addAccountForm.reset();
}

if (!created) {
  addAccountForm.addEventListener("submit", function() {
    handleSubmit(event);
  }, false);
}

function handleSubmit(event) {
  // prevent the page refresh.
  event.preventDefault();
  var data = {
    'name': addAccountForm.elements['name'].value
  };
  var headers = {
      'headers': {"X-CSRFToken": "{{ csrf_token }}"}
  };
  // hit REST endpoint.
  var url = "{% url 'accounts-rest:account-create' %}";
  axios.post(url, data, headers).then((response) => {
    // close overlay
    overlay()
    document.getElementById('errors').innerHTML = "";
    document.getElementById('errors').classList.add('hidden');
  }).catch((error) => {
    // deal with errors.
    console.log(error.response);
    document.getElementById('errors').innerHTML = 'Name: ' + error.response.data.name;
    document.getElementById('errors').classList.remove('hidden');
  }); 
}
