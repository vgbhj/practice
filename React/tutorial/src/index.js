import React from 'react'
import ReactDOM from 'react-dom/client'

import './index.css'

const BookList = () => {
  return (
    <section className="booklist">
      <Book />
      <Book />
      <Book />
      <Book />
      <Book />
    </section>
  )
}

const Book = () => {
  return (
    <article className="book">
      <Image />
      <Title />
      <Author />
    </article>
  )
}
const Image = () => (
  <img
    src="https://images-na.ssl-images-amazon.com/images/I/81bGKUa1e0L._AC_UL600_SR600,400_.jpg"
    alt="Atomic Habits"
  />
)
const Title = () => (
  <h2>
    Atomic Habits: An Easy & Proven Way to Build Good Habits & Break Bad Ones{' '}
  </h2>
)
const Author = () => {
  return <h4>by James Clear (Author)</h4>
}
const root = ReactDOM.createRoot(document.getElementById('root'))

root.render(<BookList />)
