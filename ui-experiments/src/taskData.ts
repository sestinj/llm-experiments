export interface Task {
    title: string,
    description: string,
    imageUrl: string,
    parameters: string[],
    keywords: string[]
}

export const taskData: Task[] = [
    {
        title: "Order Food",
        description: "Order food from DoorDash",
        imageUrl: "https://assets.stickpng.com/thumbs/5e8ce484664eae0004085467.png",
        parameters: [],
        keywords: ["food", "hungry", "doordash"]
    },
    {
        title: "Search Google",
        description: "Search Google for relevant websites and summarize them",
        imageUrl: "https://assets.stickpng.com/images/5847f9cbcef1014c0b5e48c8.png",
        parameters: [],
        keywords: ["wonder", "why", "how to", "google", "search", "look up"]
    },
    {
        title: "Order an Uber",
        description: "Order an Uber",
        imageUrl: "https://pngimg.com/uploads/uber/uber_PNG13.png",
        parameters: [],
        keywords: ["transportation", "car", "uber", "lyft", "ride"]
    }
];