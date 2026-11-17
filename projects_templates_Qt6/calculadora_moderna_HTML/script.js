const display = document.querySelector(".display");
const operator = document.querySelectorAll(".operator");
const number = document.querySelectorAll(".number");
const decimal = document.querySelector(".decimal");

let saveValue = "";

number.forEach((element) => {
  element.addEventListener("click", () => {
    if (saveValue == "0") {
      saveValue = "";
      saveValue += element.innerText;
      display.innerText = saveValue;
    } else {
      saveValue += element.innerText;
      display.innerText = saveValue;
    }
  });
});

operator.forEach((element) => {
  element.addEventListener("click", () => {
    let checkOpr = display.innerText.slice(-1);

    if ("+-%*/".includes(checkOpr)) {
      return;
    }
    saveValue += element.innerText;
    display.innerText = saveValue;
  });
});

// Decimal Button
decimal.addEventListener("click", () => {
  let abc = display.innerText.split(/[+%*/-]/).pop();
  if (abc.includes(".")) {
    return;
  }

  saveValue += decimal.innerText;
  display.innerText = saveValue;
});

// Equal Button
document.querySelector(".equal").addEventListener("click", ()=>{
    saveValue = eval(display.innerText);
    display.innerText = saveValue;
})

// All Clear button
document.getElementById("clear").addEventListener("click",()=>{
    saveValue = 0;
    display.innerText = saveValue;
})

// Delete Button
document.getElementById("del").addEventListener("click",()=>{
    saveValue = display.innerText.slice(0, -1);

    if(saveValue == ""){
        display.innerText = "0"
    } else{
        display.innerText = saveValue;
    }

})