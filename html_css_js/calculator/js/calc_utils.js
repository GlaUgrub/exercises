function Calculator(data) {

  this.runtime_data = {
    acc_cap_inc: 0, // accumulated income came from initial capital
    salary: data.init_salary, // salary for current year
    acc_sal: 0, // accumulated salary from past years
    acc_sal_inc: 0 // accumulated income came from salary
  }

  function getPerc(val, perc) {
    return val * perc / 100;
  }

  this.init_summ = data.init_summ;
  this.capital_increase = data.capital_increase;
  this.brick = getPerc(data.init_summ, data.capital_increase); // yearly income comming from initial summ
  this.salary_increase = data.salary_increase;

  this.liveAYear = function () {
    var rd = this.runtime_data;

    // [1] Calculate this year income came from accumulated capital income
    var income1 = getPerc(rd.acc_cap_inc, this.capital_increase);

    // [2] Add year income to accumulated income
    rd.acc_cap_inc += income1;

    // [3] Add yearly income comming from initial summ to accumulated income
    rd.acc_cap_inc += this.brick;

    // [4] Calculate this year income came from accumulated salary
    var income2 = getPerc(rd.acc_sal, this.capital_increase);

    // [5] Add salary for this year to accumulated salary
    rd.acc_sal += rd.salary;

    // [6] Calculate salary for next year
    rd.salary += getPerc(rd.salary, this.salary_increase);

    // [7] Calculate this year income came from accumulated salary income
    var income3 = getPerc(rd.acc_sal_inc, this.capital_increase);

    // [8] Add both incomes from accumulate dsalary and from accumulated salary income to accumulated income
    rd.acc_sal_inc += income2;
    rd.acc_sal_inc += income3;

    return rd;
  }

  this.getTotal = function () {
    var rd = this.runtime_data;

    return this.init_summ + rd.acc_sal + rd.acc_cap_inc + rd.acc_sal_inc;
  }


}
