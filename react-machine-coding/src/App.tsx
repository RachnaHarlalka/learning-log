import SearchInput from "./components/SearchInput"

function App() {

  function handleOnSearch(value: string) {
    console.log({ value })
  }
  return (
    <><h2>Hello</h2>
      <SearchInput onSearch={handleOnSearch} delay={300} /></>
  )
}

export default App
