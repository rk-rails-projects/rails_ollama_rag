require 'ollama-ai'
require "chroma-db"
require "logger"

class RspecRag
  def initialize
    @model = 'deepseek-r1-8b'
    @ollama = Ollama.new(credentials: { address: 'http://localhost:11434' }, options: { server_sent_events: true })
    @chroma = Chroma::Client.new
    @collection = @chroma.get_or_create_collection(name: 'rspec_examples')
  end

  # Store examples in your vector DB
  def seed_examples
    examples = [
      {
        content: "RSpec.describe 'User' do\n  it 'validates presence of email' do\n    user = User.new(email: nil)\n    expect(user).not_to be_valid\n  end\nend",
        metadata: { type: 'model_validation', framework: 'rails' }
      },
      {
        content: "RSpec.describe 'PostsController', type: :controller do\n  describe 'GET #index' do\n    it 'returns http success' do\n      get :index\n      expect(response).to have_http_status(:success)\n    end\n  end\nend",
        metadata: { type: 'controller_test', framework: 'rails' }
      }
    ]
    
    @collection.add(
      documents: examples.map { |e| e[:content] },
      metadatas: examples.map { |e| e[:metadata] }
    )
  end

  # Retrieve similar examples
  def find_similar_examples(query, k: 3)
    @collection.query(
      query_texts: [query],
      n_results: k
    )
  end

  # Generate RSpec with context
  def generate_rspec(requirement)
    similar = find_similar_examples(requirement)
    context = similar.join("\n---\n")
    
    prompt = <<~PROMPT
      You are an expert Ruby developer specializing in RSpec. Here are some similar examples:
      #{context}

      Based on these examples and the following requirement, write a complete RSpec test:
      Requirement: #{requirement}

      Respond with only the RSpec code, no additional explanation.
    PROMPT

    @ollama.generate(model: @model, prompt: prompt)
  end
end
