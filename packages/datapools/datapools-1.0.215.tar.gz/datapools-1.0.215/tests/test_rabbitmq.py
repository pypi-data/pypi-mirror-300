import os
import asyncio
import time
import pytest
from datapools.common.queues import GenericQueue, QueueRole, QueueMessage, QueueMessageType
from datapools.common.logger import logger


@pytest.mark.anyio
async def test_rabbitmq_basic():
    wq = GenericQueue(
        role=QueueRole.Publisher,
        name="test_q",
        url=os.environ.get("QUEUE_CONNECTION_URL"),
    )
    await wq.run()
    assert await wq.is_ready(timeout=5)

    await wq.push(QueueMessage(message_type=QueueMessageType.Task, data="test"))

    rq = GenericQueue(
        role=QueueRole.Receiver,
        name="test_q",
        url=os.environ.get("QUEUE_CONNECTION_URL"),
    )
    await rq.run()
    assert await rq.is_ready(timeout=5)

    message = await rq.pop(timeout=1)
    assert message is not None
    qm = QueueMessage.decode(message.body)
    assert qm.type == QueueMessageType.Task
    assert qm.data == "test"

    await wq.delete()
    await wq.stop()
    await rq.delete()
    await rq.stop()


@pytest.mark.anyio
async def test_rabbitmq_size():
    SIZE = 10000

    wq = GenericQueue(
        role=QueueRole.Publisher,
        name="test_q",
        url=os.environ.get("QUEUE_CONNECTION_URL"),
    )
    await wq.run()
    assert await wq.is_ready(timeout=5)

    start = time.time()
    for i in range(SIZE):
        await wq.push(QueueMessage(message_type=QueueMessageType.Task, data=f"test{i}"))
    logger.info(f"pushed {SIZE} messages in {time.time()-start}")
    await asyncio.sleep(5)

    rq = GenericQueue(role=QueueRole.Receiver, name="test_q", url=os.environ.get("QUEUE_CONNECTION_URL"), size=SIZE)
    await rq.run()
    assert await rq.is_ready(timeout=5)

    start = time.time()
    for i in range(SIZE):
        # logger.info(i)
        message = await rq.pop(timeout=1)
        assert message is not None
        qm = QueueMessage.decode(message.body)
        assert qm.type == QueueMessageType.Task
        assert qm.data == f"test{i}"

        if i % 2 == 0:
            await rq.mark_done(message)
        else:
            await rq.reject(message, requeue=False)

    logger.info(f"poped {SIZE} messages in {time.time()-start}")

    # no messages left in queue
    message = await rq.pop(timeout=10)
    assert message is None

    await wq.delete()
    await wq.stop()
    await rq.stop()
