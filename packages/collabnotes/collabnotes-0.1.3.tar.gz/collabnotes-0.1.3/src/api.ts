/**
 * Fetches data from a given URL.
 * 
 * @param url The URL to fetch data from.
 * @returns A promise that resolves to the fetched data.
 */
export async function fetchData(url: string): Promise<any> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json(); // Assuming the server responds with JSON
    return data;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    return {};
  }
}