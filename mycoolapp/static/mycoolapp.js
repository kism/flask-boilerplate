function getHello() {
  const controller = new AbortController();

  const timeoutId = setTimeout(() => controller.abort(), 1000); // 1 second timeout:

  fetch("hello", {
    method: "GET",
    signal: controller.signal,
  })
    .then((response) => {
      // Check if the request was successful (status code 200)
      if (response.ok) {
        return response.json();
      } else {
        document.getElementById("MY_COOL_FIELD").innerHTML = `API FAILURE`; // Set message in element to indicate failure
        document.getElementById("MY_COOL_RESULT").innerHTML = `${response.status}`; // Set message in element to message recieved from flask
        document.getElementById("MY_COOL_RESULT").style.color = "#800000"; // Set message in element to message recieved from flask

        throw new Error(`Error fetching data. Status code: ${response.status}`);
      }
    })
    .then((data) => {
      // Get the 'msg' field from the JSON data
      const msg = data.msg;
      document.getElementById("MY_COOL_FIELD").innerHTML = `API SUCCESS`; // Set message in element to indicate success
      document.getElementById("MY_COOL_RESULT").innerHTML = msg; // Set message in element to message recieved from flask
      document.getElementById("MY_COOL_RESULT").style.color = "#008000"; // Set message in element to message recieved from flask
    })
    .catch((error) => {
      clearTimeout(timeoutId);
      if (error.name === "AbortError") {
        console.error("Fetch request timed out");
        document.getElementById("MY_COOL_FIELD").innerHTML = `API FAILURE`; // Set message in element to indicate failure
        document.getElementById("MY_COOL_RESULT").innerHTML = `Fetch Timeout`; // Set message in element to message recieved from flask
        document.getElementById("MY_COOL_RESULT").style.color = "#800000"; // Set message in element to message recieved from flask
      } else {
        console.error(`Error: ${error.message}`);
      }
    });
}

//On page load we run this code, running the function getHello()
getHello()
//We call every 5 seconds, using setInterval waits for the timeout even on the first call hence why we call it normally first
setInterval(getHello, 5000);
