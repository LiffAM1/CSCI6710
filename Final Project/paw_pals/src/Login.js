function Login() {
  return (
    <div className="App">
      <section class="">
        <div class="px-4 py-5 px-md-5 text-center text-lg-start" style="background-color: hsl(0, 0%, 96%)">
          <div class="container">
            <div class="row gx-lg-5 align-items-center">
              <div class="col-lg-6 mb-5 mb-lg-0">
                <h1 class="my-5 display-3 fw-bold ls-tight">
                  <span class="text-primary">Logo goes here</span>
                </h1>
                <p style="color: hsl(217, 10%, 50.8%)">
                  The social media for pets and their humans.
                </p>
              </div>
            </div>
          </div>
          <div class="col-lg-6 mb-5 mb-lg-0">
            <div class="card">
              <div class="card-body py-5 px-md-5">
                <h3 class="my-5 display-3 fw-bold ls-tight">
                  Log in or Sign Up!<br />
                </h3>
                <form>
                  <button type="button" class="btn btn-link btn-floating mx-1">
                    <i class="fab fa-google"></i>
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Login;
