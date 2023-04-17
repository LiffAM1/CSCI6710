import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Feed() {
    const [posts, setItems] = useState([]);

    useEffect(() => {
        (async () => {
            const friendsResponse = await axios.get("https://127.0.0.1:5000/friends/e2e4553f-3cff-4c53-bd04-acc412364952");
            const postsResponse = await axios.get("https://127.0.0.1:5000/friends/e2e4553f-3cff-4c53-bd04-acc412364952/posts");
            const newPosts = postsResponse.data;
            newPosts.forEach((post) => {
                const friend = friendsResponse.data.find((friend) => friend.id === post.pet_id);
                post.friendName = friend.name;
            });


            setItems([...posts, ...newPosts]);
        })()
        
    }, []);


    const renderedPosts = [];
    posts.forEach((post, index) => {
        renderedPosts.push(
            <li className="list-group-item" key={index}>
                <h3 className="list-group-item-heading">{post.friendName}</h3>
                <p className="list-group-item-text">{post.message}</p>
            </li>
        )
    });

    return (
        <div className="container">
            <ul className="list-group">
                {renderedPosts}
            </ul>
        </div>

    );
}

export default Feed;
