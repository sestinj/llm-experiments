<script lang="ts">
    import {taskQueue, logs} from "../store";
    import TaskCard from "../lib/TaskCard.svelte";
    import {taskData} from "../taskData";
    import type {Task} from "../taskData";

    /** Thoughts
     * What if you could include a delimeter that indicated "exact" phrases, like commands? For example, if you typed "[search]", then all of the text around it would get scooped up as context and processed by some predetermined search action. Might also want explicit parameters like "[search](how to tie a knot)".
     * 
    */

    let taskSet = new Set<Task>();

    function addLog(log: string) {
        $logs[$logs.length] = log;
    }

    type TaskFinder = (fullText: string) => Task[];
    const taskFinders = [
        (fullText: string) => {
            let tasks: Task[] = [];

            let sentences = fullText.split(".");
            let lastSentence = sentences[sentences.length - 1];

            for (let task of taskData) {
                if (taskSet.has(task)) continue;
                for (let keyword of task.keywords) {
                    if (lastSentence.includes(keyword)) {
                        tasks.push(task);
                    }
                }
            }
            return tasks;
        }
    ]

    function pinchTask(task: Task) {
        if (taskSet.has(task)) return;
        taskSet.add(task);
        $taskQueue[$taskQueue.length]= task;
        console.log(task);
    }

    function handleEvent(event: InputEvent) {
        switch (event.inputType) { 
            case "insertText":
                // console.log(event.data);
                break;
            default:
                // console.log(event.inputType);
                break;
        }

        taskFinders.forEach((taskFinder: TaskFinder) => {
            taskFinder(event.target.value).forEach((task: Task) => {
                pinchTask(task);
            })
        })
    }

</script>


<h1>{"<textarea++ />"}</h1>

<div id="magic-div-outer">
    <textarea rows="20" class="magic-textarea" on:input={handleEvent}></textarea>
    <div id="magic-div-inner">
        {#each $taskQueue as task}
            <TaskCard {task} addLog={addLog}></TaskCard>
        {/each}
    </div>
</div>

<pre class="log-output">
    {#each $logs as log}
        <div>{log}</div>
    {/each}
</pre>

<style>
    .magic-textarea {
        font-size: large;
        font-family:Verdana, Geneva, Tahoma, sans-serif;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid black;
        margin: auto;
        width: 100%;
    }

    .magic-textarea:focus {
        outline: none;
        box-shadow: 0px 0px 4px 2px yellow;
    }

    #magic-div-outer {
        display: flex;
        gap: 24px;
    }

    #magic-div-inner {
        background-color: #fff6;
        width: 50%;
        border-radius: 12px;
        /* border: 1px solid gray; */
    }

    .log-output {
        background-color: #fff6;
        border-radius: 12px;
    }
</style>