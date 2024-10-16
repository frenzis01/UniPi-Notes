#include <cstdint>
#include <thread>
#include <vector>

// uint64_t
#include <iostream>  // std :: cout std :: endl
// std :: vector
// std: :thread

// this function will be called by the threads (should be void)
void say_hello(uint64_t id) {
  std ::cout << "Hello from thread: " << id << std ::endl;
}
// this runs in the master thread
int main(int argc, char* argv[]) {
  const uint64_t num_threads{(argc == 2) ? std ::stoul(argv[1]) : 10};
  std ::vector<std ::thread> threads;

  // for all threads
  for (uint64_t id = 0; id < num_threads; id++)
    // emplace the thread object in vector threads
    // using argument forwarding, this avoids unnecessary
    // move operations to the vector after thread creation
    threads.emplace_back(
        // call say hello with argument id
        say_hello, id);

  // join each thread at the end
  for (auto& thread : threads) thread.join();
}