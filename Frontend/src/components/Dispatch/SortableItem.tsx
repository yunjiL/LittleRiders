import { useEffect, useState } from 'react'

import { UniqueIdentifier } from '@dnd-kit/core'
import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { ChildInfo } from '@types'
import { FaChild } from 'react-icons/fa'
import { MdDragHandle } from 'react-icons/md'

interface Props {
  id: UniqueIdentifier
  selectedStation?: number
  name: string
  type?: string
  index: number
  childList?: ChildInfo[]
  onClick?: (id: number) => void
  onHover?: () => void
}

export function SortableItem({
  id,
  selectedStation,
  name,
  type,
  index,
  childList,
  onClick,
}: Props) {
  const [isClicked, setIsClicked] = useState<boolean>(false)
  const [isMouseOver, setIsMouseOver] = useState<boolean>(false)
  const [childCount, setChildCount] = useState<number | undefined>(
    childList?.length,
  )
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id })

  if (childList) {
    console.log(id)
    console.log(childList)
  }

  const sortIcon = (type: string | undefined) => {
    if (!type) {
      return (
        <div className="flex w-8 justify-center">
          <MdDragHandle size={30} />
        </div>
      )
    }
    if (type === 'selectedStationList')
      return <p className="w-8 text-center text-xl font-bold">{index}</p>
    if (type === 'stationList')
      return <img src="/src/assets/image/bus-stop-icon.svg" className="w-8" />
    if (type.includes('childList')) return <></>
  }

  const childrenNumberIcon = (type: string | undefined) => {
    if (type === 'selectedStationList')
      return (
        <div className="flex items-center justify-center text-gray-500">
          <FaChild />
          <p className="w-8 text-center text-xl font-bold">{childCount}</p>
        </div>
      )
    return <></>
  }

  useEffect(() => {
    setChildCount(childList?.length)
  }, [childList])

  useEffect(() => {
    setIsClicked(selectedStation === Number(id.toString()))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedStation])
  return (
    <div
      style={{ transform: CSS.Transform.toString(transform), transition }}
      ref={setNodeRef}
      {...attributes}
      {...listeners}
      className={`m-3 h-auto w-[270px] rounded-md border-2  p-3 shadow-md transition ${isClicked ? 'border-lightgreen bg-lightgreen text-white' : isMouseOver ? 'border-lightgreen bg-white' : 'bg-white'}`}
      onClick={() => {
        if (onClick) {
          onClick(Number(id.toString()))
          console.log('clicked!')
        }
      }}
      onMouseOver={() => {
        setIsMouseOver(true)
      }}
      onMouseOut={() => {
        setIsMouseOver(false)
      }}
    >
      <div className="flex items-center justify-start">
        {sortIcon(type)}
        <div className="flex w-full justify-between">
          <p className="ms-2 text-center">{name}</p>
          {childrenNumberIcon(type)}
        </div>
      </div>
    </div>
  )
}