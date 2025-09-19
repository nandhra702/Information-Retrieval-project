const form = document.getElementById("searchForm");
  form.addEventListener("submit", function (e) {
    e.preventDefault(); // stops actual navigation to /search
    const query_input = form.query.value; // name="query"
     // call your function
  });