load("//tensorflow:tensorflow.bzl", "tf_cc_test")
load("//tensorflow:tensorflow.default.bzl", "tf_grpc_cc_dependencies")
load("//tensorflow/core/platform:rules_cc.bzl", "cc_library")

package(
    # copybara:uncomment default_applicable_licenses = ["//tensorflow:license"],
    default_visibility = [
        "//tensorflow:internal",
    ],
    licenses = ["notice"],
)

cc_library(
    name = "grpc_eager_service",
    srcs = ["grpc_eager_service.h"],
    hdrs = ["grpc_eager_service.h"],
    # copybara:uncomment copts = ["-Wthread-safety-analysis"],
    deps = [
        "//tensorflow/core/protobuf:eager_service_cc_grpc_proto",
    ] + tf_grpc_cc_dependencies(),
)

cc_library(
    name = "grpc_eager_client",
    srcs = ["grpc_eager_client.cc"],
    hdrs = ["grpc_eager_client.h"],
    # copybara:uncomment copts = ["-Wthread-safety-analysis"],
    deps = [
        ":grpc_eager_service",
        "//tensorflow/core:framework",
        "//tensorflow/core:lib",
        "//tensorflow/core:lib_internal",
        "//tensorflow/core/distributed_runtime:call_options",
        "//tensorflow/core/distributed_runtime/eager:eager_client",
        "//tensorflow/core/distributed_runtime/rpc:grpc_channel",
        "//tensorflow/core/distributed_runtime/rpc:grpc_client_cq_tag",
        "//tensorflow/core/distributed_runtime/rpc:grpc_state",
        "//tensorflow/core/distributed_runtime/rpc:grpc_util",
        "//tensorflow/core/platform:error_payloads",
        "//tensorflow/core/protobuf:eager_service_proto_cc",
        "//tensorflow/core/protobuf:for_core_protos_cc",
        "@com_google_absl//absl/log",
        "@com_google_absl//absl/status",
        "@local_xla//xla/tsl/distributed_runtime:call_options",
    ] + tf_grpc_cc_dependencies(),
)

cc_library(
    name = "grpc_eager_service_impl",
    srcs = ["grpc_eager_service_impl.cc"],
    hdrs = ["grpc_eager_service_impl.h"],
    # copybara:uncomment copts = ["-Wthread-safety-analysis"],
    deps = [
        ":grpc_eager_service",
        "//tensorflow/core:framework",
        "//tensorflow/core/distributed_runtime/eager:eager_service_impl",
        "//tensorflow/core/distributed_runtime/rpc:grpc_channel",
        "//tensorflow/core/distributed_runtime/rpc:grpc_util",
        "//tensorflow/core/distributed_runtime/rpc:grpc_worker_cache",
        "//tensorflow/core/protobuf:eager_service_proto_cc",
        "@com_google_absl//absl/log",
        "@com_google_absl//absl/status",
        "@local_xla//xla/tsl/distributed_runtime/rpc:async_service_interface",
        "@local_xla//xla/tsl/distributed_runtime/rpc:grpc_call",
    ] + tf_grpc_cc_dependencies(),
)

tf_cc_test(
    name = "grpc_eager_client_test",
    size = "small",
    srcs = [
        "grpc_eager_client_test.cc",
    ],
    # copybara:uncomment extra_copts = ["-Wthread-safety-analysis"],
    deps = [
        ":grpc_eager_client",
        "//tensorflow/c:tf_status_headers",
        "//tensorflow/core:test",
        "//tensorflow/core:test_main",
        "//tensorflow/core/distributed_runtime/rpc:grpc_channel",
        "//tensorflow/core/platform:blocking_counter",
        "//tensorflow/core/platform:env",
        "//tensorflow/core/platform:status",
        "//tensorflow/core/platform:strcat",
        "@com_google_absl//absl/status",
        "@local_xla//xla/tsl/protobuf:error_codes_proto_impl_cc",
    ],
)
