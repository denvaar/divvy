
var created = false;
//var addAccountForm = document.getElementById("accountCreate");

function overlay() {
  el = document.getElementById("overlay");
  el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
  addAccountForm.reset();
  document.getElementById('errors').innerHTML = "";
  document.getElementById('errors').classList.toggle('hidden');
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
    var table = document.getElementById("accountTable");
    var row = table.insertRow();
    var cellName = row.insertCell();
    var cellBalance = row.insertCell();
    cellName.innerHTML = data.name;
    cellBalance.innerHTML = "$0.00";
 }).catch((error) => {
    // deal with errors.
    document.getElementById('errors').innerHTML = getErrorList(error.response.data);
    document.getElementById('errors').classList.remove('hidden');
  }); 
}

String.prototype.cap = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

function getErrorList(data) {
  var errors = "";
  for (var key in data) {
    if (data.hasOwnProperty(key)) {
      if (key === "non_field_errors") {
        errors += `<p>${data[key]}</p>`;
      } else {
        errors += `<p>${key.cap()}: ${data[key]}</p>`;
      }
    }
  }
  return errors;
}
