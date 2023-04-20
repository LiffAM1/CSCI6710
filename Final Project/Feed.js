import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Feed() {
    const [posts, setItems] = useState([]);

    useEffect(() => {
        (async () => {
            const friendsResponse = await axios.get("https://127.0.0.1:5000/friends/e2e4553f-3cff-4c53-bd04-acc412364952");
            const postsResponse = await axios.get("https://127.0.0.1:5000/friends/e2e4553f-3cff-4c53-bd04-acc412364952/posts");
            const newPosts = postsResponse.data;

            for (const post of newPosts) {
                const commentsResponse = await axios.get("https://127.0.0.1:5000/reactions/comments/" + post.id);
                const comments = commentsResponse.data;
                const friend = friendsResponse.data.find((friend) => friend.id === post.pet_id);
                post.friendName = friend.name;

                for (const comment of comments) {
                    const commentPetId = comment.pet_id;
                    const friendComment = friendsResponse.data.find((friend) => friend.id === commentPetId.pet_id);
                    if (friendComment != null) {
                        comment.commenterName = friendComment.name;
                    }
                    else {
                        const petsResponse = await axios.get("https://127.0.0.1:5000/pets/" + commentPetId);
                        comment.commenterName = petsResponse.data.name;
                    }
                }

                post.comments = comments;
            }

            setItems([...posts, ...newPosts]);
            
        })()

    }, []);


    const renderedPosts = [];
    posts.forEach((post, index) => {
        renderedPosts.push(
            <li className="list-group-item" key={index}>
                <h3 className="list-group-item-heading">{post.friendName}</h3>
                <p className="list-group-item-text">{post.message}</p>
                <ul className="list-group">
                    <h5>Comments</h5>
                    {
                        post.comments.map((comment, mapIndex) => <li className="list-group-item" key={mapIndex}>
                            <p className="list-group-item-text">{comment.commenterName}: {comment.message}</p>
                        </li>)

                    }
                </ul>
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
