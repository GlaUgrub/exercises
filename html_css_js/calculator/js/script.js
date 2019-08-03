document.
  addEventListener("DOMContentLoaded",
    function (event) {
      var output_text = document.querySelector("#output_text");
      output_text.style.display = "none";

      function Data() {
        this.years = 4;
        this.init_summ = 15000000;
        this.capital_increase = 10;
        this.init_salary = 300000;
        this.salary_increase = 7;
      }

      function setNumberById(id, number) {
        document.querySelector(id).value = number;
      }

      function fillDefaults(defaults) {
        setNumberById("#years", defaults.years);
        setNumberById("#init_summ", defaults.init_summ);
        setNumberById("#capital_increase", defaults.capital_increase);
        setNumberById("#init_salary", defaults.init_salary);
        setNumberById("#salary_increase", defaults.salary_increase);
      }

      var data = new Data();
      fillDefaults(data);

      function parseNumberById(id) {
        return Number(document.querySelector(id).value);
      }

      function parseData() {
        data.years = parseNumberById("#years");
        data.init_summ = parseNumberById("#init_summ");
        data.capital_increase = parseNumberById("#capital_increase");
        var salary = parseNumberById("#init_salary");
        var salary_term = document.querySelector("#salary_term").value;
        if (salary_term === "month") {
          data.init_salary = salary * 12;
        }
        else {
          data.init_salary = salary;
        }
        data.salary_increase = parseNumberById("#salary_increase");
      }

      function calculate() {
        parseData();

        var yearly_results = [];

        var calc = new Calculator(data);
        for (var i = 0; i < data.years; i++) {
          calc.liveAYear();
          yearly_results[i] = calc.getTotal();
        }

        return yearly_results;
      }

      function outputResults(yearly) {
        var out_region = document.querySelector("#output_text");
        out_region.innerHTML = "<p>Результат:</p>";

        for (var i = 0; i < yearly.length; i++) {
          var line = "Год " + (i + 1) + ": " + yearly[i];
          out_region.innerHTML += "<p>" + line + "</p>";
        }
      }

      function doWork(event) {
        results = calculate();
        outputResults(results);
        output_text.style.display = "block";
        calcLevels(results[results.length - 1]);
      }

      document.querySelector("button").addEventListener("click", doWork);
    }
  )
