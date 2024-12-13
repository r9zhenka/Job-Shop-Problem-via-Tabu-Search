import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# диаграмма Гантта
def Gantt(job_shop_data, filename = 'Unknown', stats=None, benchmark_makespan = None):
    """
    Строит диаграмму Гантта для Job Shop Problem.
    """
    num_machines = len(job_shop_data)
    colors = plt.cm.tab20.colors  # берем готовую палитру

    fig, ax = plt.subplots(figsize=(10, 6))

    # Перебираем машины
    for machine_index, machine_operations in enumerate(job_shop_data):
        for operation in machine_operations:
            start, end, job_id = operation
            ax.barh(machine_index, end - start, left=start, color=colors[job_id % len(colors)], edgecolor='black', height=0.8)

    ax.set_yticks(range(num_machines))
    ax.set_yticklabels([f"Machine {i}" for i in range(num_machines)])
    ax.set_xlabel("Time")
    ax.set_title(f"Gantt Chart for file: '{filename}'")

    # legend
    job_ids = sorted(set(op[2] for machine in job_shop_data for op in machine))
    job_patches = [mpatches.Patch(color=colors[job_id % len(colors)], label=f"Job {job_id}") for job_id in job_ids]
    benchmark_patch = None
    if benchmark_makespan is not None:
        ax.axvline(x=benchmark_makespan, color='red', linestyle='--', linewidth=2)
        benchmark_patch = mpatches.Patch(color='red', label=f"Benchmark: {benchmark_makespan}")

    all_patches = job_patches
    if benchmark_patch:
        all_patches.append(benchmark_patch)

    ax.legend(handles=all_patches, title="Legend", bbox_to_anchor=(1.05, 1), loc="upper left")

    if stats:
        stats['dimension'] = f'{num_machines}x{len(job_ids)}'
        stats_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
        ax.text(
            1.05, 1.1, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5)
        )

    plt.tight_layout()
    plt.show()

