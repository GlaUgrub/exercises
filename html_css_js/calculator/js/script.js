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

        var calculated_data = {
          yearly: yearly_results,
          calculator: calc
        }

        return calculated_data;
      }

      function outputResults(calculated_data) {
        var out_region = document.querySelector("#output_text");
        out_region.innerHTML = "<p>Результат:</p>";

        var yearly = calculated_data.yearly;
        for (var i = 0; i < yearly.length; i++) {
          var line = "Год " + (i + 1) + ": " + numberWithCommas(yearly[i]);
          out_region.innerHTML += "<p>" + line + "</p>";
        }

        // var result = calculated_data.calculator.runtime_data;
        // var total = "Income from capital = " + result.acc_cap_inc + ", Salary = " + result.acc_sal + ", Income from salary = " + result.acc_sal_inc;
        // out_region.innerHTML += "<p>" + total + "</p>";

      }

      function doWork(event) {
        results = calculate();
        outputResults(results);
        output_text.style.display = "block";

        var grand_total = results.calculator.getTotal();

        var calc = results.calculator;
        var init_summ = calc.init_summ;
        var nums = calc.runtime_data;

        var my_chart = new Chart(grand_total, 5, "#chart");
        my_chart.drawGrid("#000000");

        var bars = {
          init_sum: {
            height: init_summ,
            color: "#003f5c",
            text: numberWithCommas(init_summ),
            legend: "Начальный капитал"
          },
          acc_cap_inc: {
            height: nums.acc_cap_inc,
            color: "#58508d",
            text: numberWithCommas(nums.acc_cap_inc),
            legend: "Доход от инвестирования начального капитала"
          },
          acc_sal: {
            height: nums.acc_sal,
            color: "#bc5090",
            text: numberWithCommas(nums.acc_sal),
            legend: "Зарплата"
          },
          acc_sal_inc: {
            height: nums.acc_sal_inc,
            color: "#ff6361",
            text: numberWithCommas(nums.acc_sal_inc),
            legend: "Доход от инвестирования зарплаты"
          }
        };

        var blocks_for_joint_bar = []

        for (var bar in bars) {
          var blocks = [bars[bar]];
          my_chart.addBar(blocks);

          blocks_for_joint_bar[bar] = bars[bar];
        }

        my_chart.addBar(blocks_for_joint_bar);

        var legend = document.querySelector("legend[for='chart']");
        if (!legend.hasChildNodes()) {
          var ul = document.createElement("ul");
          legend.append(ul);
          for (var bar in bars) {
            var li = document.createElement("li");
            li.style.listStyle = "none";
            li.style.borderLeft = "20px solid " + bars[bar].color;
            li.style.padding = "5px";
            li.textContent = bars[bar].legend;
            ul.append(li);
          }
        }
      }

      document.querySelector("button").addEventListener("click", doWork);
    }
  )
