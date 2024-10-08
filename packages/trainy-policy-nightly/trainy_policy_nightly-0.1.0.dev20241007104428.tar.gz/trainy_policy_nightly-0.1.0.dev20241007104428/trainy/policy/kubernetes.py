import subprocess

import sky


def update_current_kubernetes_clusters_from_registry():
    """Mock implementation of updating kubernetes clusters from registry."""
    # All cluster names can be fetched from an organization's internal API.
    NEW_CLUSTER_NAMES = ["my-cluster"]
    for cluster_name in NEW_CLUSTER_NAMES:
        # Update the local kubeconfig with the new cluster credentials.
        subprocess.run(
            f"gcloud container clusters get-credentials {cluster_name} "
            "--region us-central1-c",
            shell=True,
            check=False,
        )


def get_allowed_contexts():
    """Mock implementation of getting allowed kubernetes contexts."""
    from sky.provision.kubernetes import utils

    contexts = utils.get_all_kube_config_context_names()
    return contexts[:2]


class DynamicKubernetesContextsUpdatePolicy(sky.AdminPolicy):
    """Example policy: update the kubernetes context to use."""

    @classmethod
    def validate_and_mutate(
        cls, user_request: sky.UserRequest
    ) -> sky.MutatedUserRequest:
        """Updates the kubernetes context to use."""
        # Append any new kubernetes clusters in local kubeconfig. An example
        # implementation of this method can be:
        #  1. Query an organization's internal Kubernetes cluster registry,
        #     which can be some internal API, or a secret vault.
        #  2. Append the new credentials to the local kubeconfig.
        update_current_kubernetes_clusters_from_registry()
        # Get the allowed contexts for the user. Similarly, it can retrieve
        # the latest allowed contexts from an organization's internal API.
        allowed_contexts = get_allowed_contexts()

        # Update the kubernetes allowed contexts in skypilot config.
        config = user_request.skypilot_config
        config.set_nested(("kubernetes", "allowed_contexts"), allowed_contexts)
        return sky.MutatedUserRequest(task=user_request.task, skypilot_config=config)
