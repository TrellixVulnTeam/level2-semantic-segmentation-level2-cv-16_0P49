_base_ = "./ocrnet_base.py"
norm_cfg = dict(type="SyncBN", requires_grad=True)
model = dict(
    pretrained="open-mmlab://msra/hrnetv2_w48",
    backbone=dict(
        extra=dict(
            stage2=dict(num_channels=(48, 96)),
            stage3=dict(num_channels=(48, 96, 192)),
            stage4=dict(num_channels=(48, 96, 192, 384)),
        )
    ),
    decode_head=[
        dict(
            type="FCNHead",
            in_channels=[48, 96, 192, 384],
            channels=sum([48, 96, 192, 384]),
            input_transform="resize_concat",
            in_index=(0, 1, 2, 3),
            kernel_size=1,
            num_convs=1,
            norm_cfg=norm_cfg,
            concat_input=False,
            dropout_ratio=-1,
            num_classes=19,
            align_corners=False,
            loss_decode=dict(
                type="CrossEntropyLoss", use_sigmoid=False, loss_weight=0.4
            ),
        ),
        dict(
            type="OCRHead",
            in_channels=[48, 96, 192, 384],
            channels=512,
            ocr_channels=256,
            input_transform="resize_concat",
            in_index=(0, 1, 2, 3),
            norm_cfg=norm_cfg,
            dropout_ratio=-1,
            num_classes=19,
            align_corners=False,
            loss_decode=dict(
                type="CrossEntropyLoss", use_sigmoid=False, loss_weight=1.0
            ),
        ),
    ],
)

optimizer = dict(type="SGD", lr=0.1, momentum=0.9, weight_decay=0.0005)

log_config = dict(
    interval=150,
    hooks=[
        dict(type="TextLoggerHook", by_epoch=True),
        dict(
            type="WandbLoggerHook",
            init_kwargs=dict(
                entity="medic", project="semantic-segmentation", name="DB_ocrnet_lr0.1"
            ),
        )
        # dict(type='TensorboardLoggerHook')
    ],
)
