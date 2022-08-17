<script lang="ts">
    import type {Task} from "../taskData";

    export let task: Task;
    export let addLog: (log: string) => void;
    export let tabindex: number;

    const timing = 5;

    let selfRef: HTMLDivElement;

    let cleared = false;

    let timer = setTimeout(() => {
        selfRef.remove();
    }, timing * 1000)

</script>

<div class="task-card" {tabindex} bind:this={selfRef} on:click={() => {
    clearTimeout(timer);
    cleared = true;
    addLog(`Executing task: ${task.title}`);
    selfRef.remove();
}}>
    <div class="task-contents">
        <img src={task.imageUrl} alt={task.title} class="task-card-img">
        <div>
            <b>{task.title}</b>
            <p>{task.description}</p>
        </div>
    </div>
    
    <div class="loader" style="--timing: {timing}s" hidden={cleared}></div>
</div>

<style>
    .task-card {
        padding: 8px;
        margin: 8px;
        /* border: 1px solid black; */
        border-radius: 8px;
        background-color: #fff8;
        box-shadow: 0px 0px 2px 0px;
        overflow: hidden;
        cursor: pointer;
    }

    .task-contents {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .loader {
        bottom: 0px;
        background-color: #80f;
        height: 4px;
        margin: -8px;

        animation-name: loader-width;
        animation-duration: var(--timing);
        animation-timing-function: linear;
    }

    @keyframes loader-width {
        from {
            width: 0%;
        }
        to {
            width: calc(100% + 16px);
        }
    }

    .task-card-img {
        width: 20%;
    }
</style>