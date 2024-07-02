function getHello() {
  fetch("hello", {
    method: "GET",
  })
    .then((response) => {
      // Check if the request was successful (status code 200)
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(`Error fetching data. Status code: ${response.status}`);
      }
    })
    .then((data) => {
      // Get the 'msg' field from the JSON data
      const msg = data.msg;

      document.getElementById("MY_COOL_FIELD").innerHTML = `API SUCCESS`;

      document.getElementById("MY_COOL_RESULT").innerHTML = msg;
      document.getElementById("MY_COOL_RESULT").style.color = "#008000";
    })
    .catch((error) => {
      console.error(`Error: ${error.message}`);
    });
}

getHello();
