export function debouncedSearchFn(fn: Function, delay: number) {
  let timer: number;
  return (...args: any) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn(...args);
    }, delay);
  };
}
