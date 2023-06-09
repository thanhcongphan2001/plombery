import { useState } from 'react'
import {
  Bold,
  Button,
  Card,
  Flex,
  Icon,
  List,
  ListItem,
  Text,
  Title,
} from '@tremor/react'
import { TableCellsIcon } from '@heroicons/react/24/outline'

import { Pipeline, PipelineRun } from '@/types'
import { STATUS_COLORS, STATUS_ICONS, getTasksColors } from '@/utils'
import DataViewerDialog from './DataViewerDialog'

interface Props {
  pipeline: Pipeline
  run: PipelineRun
}

const RunsTasksList: React.FC<Props> = ({ pipeline, run }) => {
  const [viewDataDialog, setViewDataDialog] = useState<string | undefined>()

  const tasksColors = getTasksColors(pipeline.tasks)

  return (
    <Card>
      <DataViewerDialog
        runId={run.id}
        taskId={viewDataDialog || ''}
        open={!!viewDataDialog}
        onClose={() => setViewDataDialog(undefined)}
      />

      <Title>Tasks</Title>

      <List>
        {pipeline.tasks.map((task, i) => (
          <ListItem key={task.id} className="space-x-4">
            {run.tasks_run && run.tasks_run[i] ? (
              <Icon
                variant="light"
                icon={STATUS_ICONS[run.tasks_run[i].status]}
                color={STATUS_COLORS[run.tasks_run[i].status]}
              />
            ) : (
              <Icon
                variant="light"
                icon={STATUS_ICONS.notrun}
                color={STATUS_COLORS.notrun}
              />
            )}
            <div className="truncate flex-grow">
              <Flex className="justify-start">
                <div
                  className={`h-2 w-2 mr-2 rounded-full ${
                    tasksColors[task.id]
                  }`}
                />
                <Text className="truncate">
                  <Bold>{task.name}</Bold>
                </Text>
              </Flex>
              {task.description && (
                <Text className="truncate">{task.description}</Text>
              )}
            </div>

            {run.tasks_run && run.tasks_run[i]?.has_output && (
              <Button
                variant="light"
                color="indigo"
                size="xs"
                icon={TableCellsIcon}
                onClick={() => setViewDataDialog(task.id)}
              >
                Data
              </Button>
            )}
          </ListItem>
        ))}
      </List>
    </Card>
  )
}

export default RunsTasksList
