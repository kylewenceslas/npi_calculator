import './App.css';
import axios from 'axios';
import { useState } from "react";

axios.defaults.baseURL = 'http://localhost:8000/';

function App() {
  const [stack, setStack] = useState([]);
  const [result, setResult] = useState("");
  const [savingCsvStatus, setSavingCsvStatus] = useState("");

  function handleInputKeyUp(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
      addNumberToStack();
    }
  }

  function addNumberToStack() {
    const number = document.getElementById("number").value.trim();    // we shall use a form rather than id in a real project
    if(number) { 
      setStack(stack.concat(number));
    }
    document.getElementById("number").value = "";
  }

  function handleSubmit() {
    axios.post('/calc', stack)
    .then(function (response) {
      setResult(response.data);
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  function saveDataToCSV() {
    setSavingCsvStatus("... saving file");
    axios.post('/save-data')
    .then(function () {
      setTimeout(() => {
        setSavingCsvStatus("File saved to data.csv");
      }, 500);
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  return (
    <div className="App">
      {Array.from({length: 10}, (_,i) => (<br key={i}/>))}
      Stack: &nbsp; {stack.join(" ")} 
        <br/>
      Number: &nbsp;
        <input 
          type="number" 
          id="number" 
          min="0"
          onKeyUp={handleInputKeyUp}
        />
        <button 
          className="App-button" 
          onClick={addNumberToStack}
        >
          Add to stack
        </button>
        <br/>
      Operation: 
        {["+", "-", "*", "/"].map((op, i) => (
          <button 
            className="App-button" 
            key={i}
            onClick={() => { setStack(stack.concat(op)) }}
          >
            {op}
          </button>  
        ))}
        <br/>
      <button 
        className="App-button" 
        onClick={() => { setStack([]) }}
      >
        Reset Stack
      </button><br/>
      <button 
        className="App-button" 
        onClick={handleSubmit}
      >
        Submit
      </button><br/>
      Result: {result}
      
      {Array.from({length: 5}, (_,i) => (<br key={i}/>))}
      <button 
        className="App-button" 
        onClick={saveDataToCSV}
      >
        Save data to CSV
      </button>
      {savingCsvStatus}
    </div>
  );
}

export default App;
