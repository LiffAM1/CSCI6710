$(document).ready(async function () {
    try {
        const friendsResponse = await $.get("https://127.0.0.1:5000/friends/e2e4553f-3cff-4c53-bd04-acc412364952");
        const postsResponse = await $.get("https://127.0.0.1:5000/friends/e2e4553f-3cff-4c53-bd04-acc412364952/posts");
        const newPosts = postsResponse;

        for (const post of newPosts) {
            const commentsResponse = await $.get("https://127.0.0.1:5000/reactions/comments/" + post.id);
            const comments = commentsResponse;
            const friend = friendsResponse.find((friend) => friend.id === post.pet_id);
            post.friendName = friend.name;

            for (const comment of comments) {
                const commentPetId = comment.pet_id;
                const friendComment = friendsResponse.find((friend) => friend.id === commentPetId.pet_id);
                if (friendComment != null) {
                    comment.commenterName = friendComment.name;
                }
                else {
                    const petsResponse = await $.get("https://127.0.0.1:5000/pets/" + commentPetId);
                    comment.commenterName = petsResponse.name;
                }
            }

            post.comments = comments;
        }

        var commentContainer = document.getElementById("comment-container");
        newPosts.forEach((post) => {
            var newPost = document.createElement("div");
            newPost.className = "d-flex flex-start";
            newPost.innerHTML = getPost(post);
            commentContainer.append(newPost);
        });
    }
    catch (error) {
        console.log(error)
    }
});

function getPost(post) {
    const comments = [];

    post.comments.forEach((comment) => {
        comments.push(`<div class="d-flex flex-start mt-4">
        
            <img class="rounded-circle shadow-1-strong me-3"
            src="" alt="avatar" width="65"
            height="65" />
        <div class="flex-grow-1 flex-shrink-1">
          <div>
            <div class="d-flex justify-content-between align-items-center">
              <p class="mb-1">
                ${comment.commenterName} <span class="small">- 3 hours ago</span>
              </p>
            </div>
            <p class="small mb-0">
              ${comment.message}
            </p>
          </div>
        </div>
      </div>`);
    })


    return ` 
    <img class="rounded-circle shadow-1-strong me-3"
      src="" alt="avatar" width="65"
      height="65" />
    <div class="flex-grow-1 flex-shrink-1">
      <div>
        <div class="d-flex justify-content-between align-items-center">
          <p class="mb-1">
            ${post.friendName} <span class="small">- 2 hours ago</span>
          </p>
          <a href="#!"><i class="fas fa-reply fa-xs"></i><span class="small"> reply</span></a>
        </div>
        <p class="small mb-0">
          ${post.message}
        </p>
      </div>

      ${comments}

      
    </div>`
}