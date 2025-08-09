import { useState } from 'react'
import bacon from './assets/images/bacon-pixelart.png'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL;


function App() {
    const [bacon_distance, setBaconDistance] = useState(Infinity)
    const [query, setQuery] = useState('')
    const handleActorSearchChange = (event) => {
        setQuery(event.target.value)
        console.log('Search query:', event.target.value) // TODO: show possible actors
    }

    const handleOnSearchClick = () => {
        fetch(`${API_URL}/api/get_bacon_distance?actor=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                setBaconDistance(data.result);
            })
            .catch(err => console.error(err));

    }

  return (
    <>
      <div className="top-left">
        <a>
          <img src={bacon} className="logo" alt="Vite logo" align={'left'}/>
        </a>
      </div>
      <div className="top-right">
          <a href="https://react.dev" target="_blank">
              <img src={bacon} className="logo react" alt="React logo" />
          </a>
      </div>
        <h1>Bacon Distance Calculator!</h1>
      <div>
          <input
              type="text"
              placeholder="Kirk Douglas"
              value={query}
              onChange={handleActorSearchChange}
          />
      </div>
      <div className="card">
        <button onClick={handleOnSearchClick}>
          Bacon Distance: {bacon_distance}
        </button>
        <p>
          What's the longest distance you can find?!
        </p>
      </div>
      <a href={"https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon"} className="read-the-docs" >
        Click here to learn more about the Bacon Distance!
      </a>
    </>
  )
}

export default App
