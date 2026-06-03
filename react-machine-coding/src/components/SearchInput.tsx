import { useEffect, useRef, useState } from "react"
import { debouncedSearchFn } from "../utils/debouncedSearchFn"

interface ISearchInput {
    placeholder?: string;
    onSearch: (value: string) => void;
    delay?: number
}

const SearchInput = ({ placeholder = "search", onSearch, delay = 300 }: ISearchInput) => {
    const [search, setSearch] = useState("")

    const debounceSearch = useRef(
        debouncedSearchFn((value: string) => {
            onSearch(value)
        }, delay)
    )


    return (
        <input
            type="text"
            placeholder={placeholder}
            onChange={(e) => { setSearch(e.target.value), debounceSearch.current(e.target.value) }}
            value={search}
        />
    )
}

export default SearchInput