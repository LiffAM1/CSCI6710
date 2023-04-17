import ReactDOM from 'react-dom';
import {
  BrowserRouter, Route, Routes, useNavigate,
} from 'react-router-dom';
import Layout from './Layout';
import Home from './Home';
import Feed from './Feed';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="feed" element={<Feed />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
